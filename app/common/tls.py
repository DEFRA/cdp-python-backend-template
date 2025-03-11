import ssl
import base64
import os
import base64
import tempfile

from logging import getLogger

logger = getLogger(__name__)


def extract_all_certs():
    certs = {}
    for var_name, var_value in os.environ.items():
        if var_name.startswith("TRUSTSTORE_"):
            try:
                decoded_value = base64.b64decode(var_value)
            except base64.binascii.Error:
                logger.error(f"Error decoding value for {var_name}. Skipping.")
                continue
            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, prefix=var_name, suffix=".pem"
            ) as tmp_file:
                tmp_file.write(decoded_value)
                logger.info(f"Written decoded value of {var_name} to {tmp_file.name}")
                certs[var_name] = tmp_file.name
    return certs


def load_certs_into_context(certs):
    ctx = ssl.create_default_context()
    for key in certs:
        try:
            ctx.load_verify_locations(certs[key])
            logger.info(f"Added {key} to truststore")
        except Exception as err:
            logger.error(f"Failed to load cert {cert}: {err}")
    return ctx


cacerts = extract_all_certs()
ctx = load_certs_into_context(cacerts)
