import kerberos
import requests
import traceback


class KerberosClient:
    class Client:
        def __init__(self, url) -> None:
            self.headers = {}
            self.url = url

        def set_auth_header(self, negotiate_details):
            self.headers["Authorization"] = "Negotiate " + negotiate_details

        def call(self) -> requests.Response:
            pass

    class GetClient(Client):
        def __init__(self, url):
            super().__init__(url)

        def call(self) -> requests.Response:
            return requests.get(self.url, headers=self.headers)

    class PostClient(Client):
        def __init__(self, url, data):
            super().__init__(url)
            self.data = data

        def call(self) -> requests.Response:
            return requests.post(self.url, headers=self.headers, data=self.data)

    class UploadFileClient(Client):
        def __init__(self, url, file_path, dest_path):
            super().__init__(url)
            # Read the file to be uploaded
            self.file_path = file_path
            self.dest_path = dest_path

        def call(self) -> requests.Response:
            with open(self.file_path, 'rb') as file:
                files = {'file': file}
                data = {'dest_path': self.dest_path}
                return requests.post(self.url, files=files, data=data, headers=self.headers)

    def __init__(self, service):
        self.service = service

    def get_service_authenticator_from_response(r: requests.Response):
        auth_header = r.headers["WWW-Authenticate"]
        # auth_header is under the form negotiate {service_authenticator}
        return auth_header.split(" ")[1]

    def kerberos_handshake(self, client: Client):
        try:
            _, krb_context = kerberos.authGSSClientInit(self.service)
            kerberos.authGSSClientStep(krb_context, "")
            # grab the service ticket
            negotiate_details = kerberos.authGSSClientResponse(krb_context)
            # setup the auth header to use the kerberos ticket
            client.set_auth_header(negotiate_details=negotiate_details)

            # make the request
            response = client.call()

            # authenticate the service
            service_auth = KerberosClient.get_service_authenticator_from_response(
                response)
            kerberos.authGSSClientStep(krb_context, service_auth)
            kerberos.authGSSClientClean(krb_context)

            return response
        except Exception:
            return None

    def get(self, url):
        client = KerberosClient.GetClient(url)
        return self.kerberos_handshake(client)

    def post(self, url, data):
        client = KerberosClient.PostClient(url, data)
        return self.kerberos_handshake(client)

    def upload_file(self, url, file_path, dest_path):
        client = KerberosClient.UploadFileClient(url, file_path, dest_path)
        return self.kerberos_handshake(client)
