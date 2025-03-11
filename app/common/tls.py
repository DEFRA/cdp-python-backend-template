import base64
import os
import ssl
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
                logger.error("Error decoding value for %s. Skipping.", var_name)
                continue
            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, prefix=var_name, suffix=".pem"
            ) as tmp_file:
                tmp_file.write(decoded_value)
                certs[var_name] = tmp_file.name
                logger.error("Error decoding value for %s. Skipping.", var_name)

    return certs


def load_certs_into_context(certs):
    ctx = ssl.create_default_context()
    for key in certs:
        try:
            ctx.load_verify_locations(certs[key])
            logger.info("Added %s to truststore", key)
        except Exception as err:
            logger.error("Failed to load cert %s: %s", key, err)
    return ctx


cacerts = extract_all_certs()
ctx = load_certs_into_context(cacerts)
