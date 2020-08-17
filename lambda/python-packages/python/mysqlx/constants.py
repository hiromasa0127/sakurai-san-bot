# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is also distributed with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation.  The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have included with
# MySQL.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

"""Constants."""

from collections import namedtuple


# pylint: disable=C0103
def create_enum(name, fields, values=None):
    """Emulates an enum by creating a namedtuple.

    Args:
        name (string): The type name.
        fields (tuple): The fields names.
        values (tuple): The values of the fields.

    Returns:
        namedtuple: A namedtuple object.
    """
    Enum = namedtuple(name, fields)
    if values is None:
        return Enum(*fields)
    return Enum(*values)


SSLMode = create_enum("SSLMode",
                      ("REQUIRED", "DISABLED", "VERIFY_CA", "VERIFY_IDENTITY"),
                      ("required", "disabled", "verify_ca", "verify_identity"))
Auth = create_enum("Auth",
                   ("PLAIN", "MYSQL41", "SHA256_MEMORY"),
                   ("plain", "mysql41", "sha256_memory"))
LockContention = create_enum("LockContention",
                             ("DEFAULT", "NOWAIT", "SKIP_LOCKED"), (0, 1, 2))

TLS_VERSIONS = ["TLSv1", "TLSv1.1", "TLSv1.2", "TLSv1.3"]

# TLS v1.0 cipher suites IANI to OpenSSL name translation
TLSV1_CIPHER_SUITES = {
    "TLS_RSA_WITH_NULL_MD5": "NULL-MD5",
    "TLS_RSA_WITH_NULL_SHA": "NULL-SHA",
    "TLS_RSA_WITH_RC4_128_MD5": "RC4-MD5",
    "TLS_RSA_WITH_RC4_128_SHA": "RC4-SHA",
    "TLS_RSA_WITH_IDEA_CBC_SHA": "IDEA-CBC-SHA",
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA": "DES-CBC3-SHA",

    "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA": "Not implemented.",
    "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA": "Not implemented.",
    "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA": "DHE-DSS-DES-CBC3-SHA",
    "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA": "DHE-RSA-DES-CBC3-SHA",

    "TLS_DH_anon_WITH_RC4_128_MD5": "ADH-RC4-MD5",
    "TLS_DH_anon_WITH_3DES_EDE_CBC_SHA": "ADH-DES-CBC3-SHA",

    # AES cipher suites from RFC3268, extending TLS v1.0
    "TLS_RSA_WITH_AES_128_CBC_SHA": "AES128-SHA",
    "TLS_RSA_WITH_AES_256_CBC_SHA": "AES256-SHA",

    "TLS_DH_DSS_WITH_AES_128_CBC_SHA": "DH-DSS-AES128-SHA",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA": "DH-DSS-AES256-SHA",
    "TLS_DH_RSA_WITH_AES_128_CBC_SHA": "DH-RSA-AES128-SHA",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA": "DH-RSA-AES256-SHA",

    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA": "DHE-DSS-AES128-SHA",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA": "DHE-DSS-AES256-SHA",
    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA": "DHE-RSA-AES128-SHA",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA": "DHE-RSA-AES256-SHA",

    "TLS_DH_anon_WITH_AES_128_CBC_SHA": "ADH-AES128-SHA",
    "TLS_DH_anon_WITH_AES_256_CBC_SHA": "ADH-AES256-SHA",

    # Camellia cipher suites from RFC4132, extending TLS v1.0
    "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA": "CAMELLIA128-SHA",
    "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA": "CAMELLIA256-SHA",

    "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA": "DH-DSS-CAMELLIA128-SHA",
    "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA": "DH-DSS-CAMELLIA256-SHA",
    "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA": "DH-RSA-CAMELLIA128-SHA",
    "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA": "DH-RSA-CAMELLIA256-SHA",

    "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA": "DHE-DSS-CAMELLIA128-SHA",
    "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA": "DHE-DSS-CAMELLIA256-SHA",
    "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA": "DHE-RSA-CAMELLIA128-SHA",
    "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA": "DHE-RSA-CAMELLIA256-SHA",

    "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA": "ADH-CAMELLIA128-SHA",
    "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA": "ADH-CAMELLIA256-SHA",

    # SEED cipher suites from RFC4162, extending TLS v1.0
    "TLS_RSA_WITH_SEED_CBC_SHA": "SEED-SHA",

    "TLS_DH_DSS_WITH_SEED_CBC_SHA": "DH-DSS-SEED-SHA",
    "TLS_DH_RSA_WITH_SEED_CBC_SHA": "DH-RSA-SEED-SHA",

    "TLS_DHE_DSS_WITH_SEED_CBC_SHA": "DHE-DSS-SEED-SHA",
    "TLS_DHE_RSA_WITH_SEED_CBC_SHA": "DHE-RSA-SEED-SHA",

    "TLS_DH_anon_WITH_SEED_CBC_SHA": "ADH-SEED-SHA",

    # GOST cipher suites from draft-chudov-cryptopro-cptls, extending TLS v1.0
    "TLS_GOSTR341094_WITH_28147_CNT_IMIT": "GOST94-GOST89-GOST89",
    "TLS_GOSTR341001_WITH_28147_CNT_IMIT": "GOST2001-GOST89-GOST89",
    "TLS_GOSTR341094_WITH_NULL_GOSTR3411": "GOST94-NULL-GOST94",
    "TLS_GOSTR341001_WITH_NULL_GOSTR3411": "GOST2001-NULL-GOST94"}

# TLS v1.1 cipher suites IANI to OpenSSL name translation
TLSV1_1_CIPHER_SUITES = TLSV1_CIPHER_SUITES

# TLS v1.2 cipher suites IANI to OpenSSL name translation
TLSV1_2_CIPHER_SUITES = {
    "TLS_RSA_WITH_NULL_SHA256": "NULL-SHA256",

    "TLS_RSA_WITH_AES_128_CBC_SHA256": "AES128-SHA256",
    "TLS_RSA_WITH_AES_256_CBC_SHA256": "AES256-SHA256",
    "TLS_RSA_WITH_AES_128_GCM_SHA256": "AES128-GCM-SHA256",
    "TLS_RSA_WITH_AES_256_GCM_SHA384": "AES256-GCM-SHA384",

    "TLS_DH_RSA_WITH_AES_128_CBC_SHA256": "DH-RSA-AES128-SHA256",
    "TLS_DH_RSA_WITH_AES_256_CBC_SHA256": "DH-RSA-AES256-SHA256",
    "TLS_DH_RSA_WITH_AES_128_GCM_SHA256": "DH-RSA-AES128-GCM-SHA256",
    "TLS_DH_RSA_WITH_AES_256_GCM_SHA384": "DH-RSA-AES256-GCM-SHA384",

    "TLS_DH_DSS_WITH_AES_128_CBC_SHA256": "DH-DSS-AES128-SHA256",
    "TLS_DH_DSS_WITH_AES_256_CBC_SHA256": "DH-DSS-AES256-SHA256",
    "TLS_DH_DSS_WITH_AES_128_GCM_SHA256": "DH-DSS-AES128-GCM-SHA256",
    "TLS_DH_DSS_WITH_AES_256_GCM_SHA384": "DH-DSS-AES256-GCM-SHA384",

    "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256": "DHE-RSA-AES128-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256": "DHE-RSA-AES256-SHA256",
    "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256": "DHE-RSA-AES128-GCM-SHA256",
    "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384": "DHE-RSA-AES256-GCM-SHA384",

    "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256": "DHE-DSS-AES128-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256": "DHE-DSS-AES256-SHA256",
    "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256": "DHE-DSS-AES128-GCM-SHA256",
    "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384": "DHE-DSS-AES256-GCM-SHA384",

    "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256": "ECDHE-RSA-AES128-SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384": "ECDHE-RSA-AES256-SHA384",
    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256": "ECDHE-RSA-AES128-GCM-SHA256",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": "ECDHE-RSA-AES256-GCM-SHA384",

    "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256": "ECDHE-ECDSA-AES128-SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384": "ECDHE-ECDSA-AES256-SHA384",
    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256": "ECDHE-ECDSA-AES128-GCM-SHA256",
    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384": "ECDHE-ECDSA-AES256-GCM-SHA384",

    "TLS_DH_anon_WITH_AES_128_CBC_SHA256": "ADH-AES128-SHA256",
    "TLS_DH_anon_WITH_AES_256_CBC_SHA256": "ADH-AES256-SHA256",
    "TLS_DH_anon_WITH_AES_128_GCM_SHA256": "ADH-AES128-GCM-SHA256",
    "TLS_DH_anon_WITH_AES_256_GCM_SHA384": "ADH-AES256-GCM-SHA384",

    "RSA_WITH_AES_128_CCM": "AES128-CCM",
    "RSA_WITH_AES_256_CCM": "AES256-CCM",
    "DHE_RSA_WITH_AES_128_CCM": "DHE-RSA-AES128-CCM",
    "DHE_RSA_WITH_AES_256_CCM": "DHE-RSA-AES256-CCM",
    "RSA_WITH_AES_128_CCM_8": "AES128-CCM8",
    "RSA_WITH_AES_256_CCM_8": "AES256-CCM8",
    "DHE_RSA_WITH_AES_128_CCM_8": "DHE-RSA-AES128-CCM8",
    "DHE_RSA_WITH_AES_256_CCM_8": "DHE-RSA-AES256-CCM8",
    "ECDHE_ECDSA_WITH_AES_128_CCM": "ECDHE-ECDSA-AES128-CCM",
    "ECDHE_ECDSA_WITH_AES_256_CCM": "ECDHE-ECDSA-AES256-CCM",
    "ECDHE_ECDSA_WITH_AES_128_CCM_8": "ECDHE-ECDSA-AES128-CCM8",
    "ECDHE_ECDSA_WITH_AES_256_CCM_8": "ECDHE-ECDSA-AES256-CCM8",

    # ARIA cipher suites from RFC6209, extending TLS v1.2
    "TLS_RSA_WITH_ARIA_128_GCM_SHA256": "ARIA128-GCM-SHA256",
    "TLS_RSA_WITH_ARIA_256_GCM_SHA384": "ARIA256-GCM-SHA384",
    "TLS_DHE_RSA_WITH_ARIA_128_GCM_SHA256": "DHE-RSA-ARIA128-GCM-SHA256",
    "TLS_DHE_RSA_WITH_ARIA_256_GCM_SHA384": "DHE-RSA-ARIA256-GCM-SHA384",
    "TLS_DHE_DSS_WITH_ARIA_128_GCM_SHA256": "DHE-DSS-ARIA128-GCM-SHA256",
    "TLS_DHE_DSS_WITH_ARIA_256_GCM_SHA384": "DHE-DSS-ARIA256-GCM-SHA384",
    "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256": "ECDHE-ECDSA-ARIA128-GCM-SHA256",
    "TLS_ECDHE_ECDSA_WITH_ARIA_256_GCM_SHA384": "ECDHE-ECDSA-ARIA256-GCM-SHA384",
    "TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256": "ECDHE-ARIA128-GCM-SHA256",
    "TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384": "ECDHE-ARIA256-GCM-SHA384",
    "TLS_PSK_WITH_ARIA_128_GCM_SHA256": "PSK-ARIA128-GCM-SHA256",
    "TLS_PSK_WITH_ARIA_256_GCM_SHA384": "PSK-ARIA256-GCM-SHA384",
    "TLS_DHE_PSK_WITH_ARIA_128_GCM_SHA256": "DHE-PSK-ARIA128-GCM-SHA256",
    "TLS_DHE_PSK_WITH_ARIA_256_GCM_SHA384": "DHE-PSK-ARIA256-GCM-SHA384",
    "TLS_RSA_PSK_WITH_ARIA_128_GCM_SHA256": "RSA-PSK-ARIA128-GCM-SHA256",
    "TLS_RSA_PSK_WITH_ARIA_256_GCM_SHA384": "RSA-PSK-ARIA256-GCM-SHA384",

    # Camellia HMAC-Based cipher suites from RFC6367, extending TLS v1.2
    "TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-ECDSA-CAMELLIA128-SHA256",
    "TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-ECDSA-CAMELLIA256-SHA384",
    "TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-RSA-CAMELLIA128-SHA256",
    "TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-RSA-CAMELLIA256-SHA384",

    # Pre-shared keying (PSK) cipher suites",
    "PSK_WITH_NULL_SHA": "PSK-NULL-SHA",
    "DHE_PSK_WITH_NULL_SHA": "DHE-PSK-NULL-SHA",
    "RSA_PSK_WITH_NULL_SHA": "RSA-PSK-NULL-SHA",

    "PSK_WITH_RC4_128_SHA": "PSK-RC4-SHA",
    "PSK_WITH_3DES_EDE_CBC_SHA": "PSK-3DES-EDE-CBC-SHA",
    "PSK_WITH_AES_128_CBC_SHA": "PSK-AES128-CBC-SHA",
    "PSK_WITH_AES_256_CBC_SHA": "PSK-AES256-CBC-SHA",

    "DHE_PSK_WITH_RC4_128_SHA": "DHE-PSK-RC4-SHA",
    "DHE_PSK_WITH_3DES_EDE_CBC_SHA": "DHE-PSK-3DES-EDE-CBC-SHA",
    "DHE_PSK_WITH_AES_128_CBC_SHA": "DHE-PSK-AES128-CBC-SHA",
    "DHE_PSK_WITH_AES_256_CBC_SHA": "DHE-PSK-AES256-CBC-SHA",

    "RSA_PSK_WITH_RC4_128_SHA": "RSA-PSK-RC4-SHA",
    "RSA_PSK_WITH_3DES_EDE_CBC_SHA": "RSA-PSK-3DES-EDE-CBC-SHA",
    "RSA_PSK_WITH_AES_128_CBC_SHA": "RSA-PSK-AES128-CBC-SHA",
    "RSA_PSK_WITH_AES_256_CBC_SHA": "RSA-PSK-AES256-CBC-SHA",

    "PSK_WITH_AES_128_GCM_SHA256": "PSK-AES128-GCM-SHA256",
    "PSK_WITH_AES_256_GCM_SHA384": "PSK-AES256-GCM-SHA384",
    "DHE_PSK_WITH_AES_128_GCM_SHA256": "DHE-PSK-AES128-GCM-SHA256",
    "DHE_PSK_WITH_AES_256_GCM_SHA384": "DHE-PSK-AES256-GCM-SHA384",
    "RSA_PSK_WITH_AES_128_GCM_SHA256": "RSA-PSK-AES128-GCM-SHA256",
    "RSA_PSK_WITH_AES_256_GCM_SHA384": "RSA-PSK-AES256-GCM-SHA384",

    "PSK_WITH_AES_128_CBC_SHA256": "PSK-AES128-CBC-SHA256",
    "PSK_WITH_AES_256_CBC_SHA384": "PSK-AES256-CBC-SHA384",
    "PSK_WITH_NULL_SHA256": "PSK-NULL-SHA256",
    "PSK_WITH_NULL_SHA384": "PSK-NULL-SHA384",
    "DHE_PSK_WITH_AES_128_CBC_SHA256": "DHE-PSK-AES128-CBC-SHA256",
    "DHE_PSK_WITH_AES_256_CBC_SHA384": "DHE-PSK-AES256-CBC-SHA384",
    "DHE_PSK_WITH_NULL_SHA256": "DHE-PSK-NULL-SHA256",
    "DHE_PSK_WITH_NULL_SHA384": "DHE-PSK-NULL-SHA384",
    "RSA_PSK_WITH_AES_128_CBC_SHA256": "RSA-PSK-AES128-CBC-SHA256",
    "RSA_PSK_WITH_AES_256_CBC_SHA384": "RSA-PSK-AES256-CBC-SHA384",
    "RSA_PSK_WITH_NULL_SHA256": "RSA-PSK-NULL-SHA256",
    "RSA_PSK_WITH_NULL_SHA384": "RSA-PSK-NULL-SHA384",

    "ECDHE_PSK_WITH_RC4_128_SHA": "ECDHE-PSK-RC4-SHA",
    "ECDHE_PSK_WITH_3DES_EDE_CBC_SHA": "ECDHE-PSK-3DES-EDE-CBC-SHA",
    "ECDHE_PSK_WITH_AES_128_CBC_SHA": "ECDHE-PSK-AES128-CBC-SHA",
    "ECDHE_PSK_WITH_AES_256_CBC_SHA": "ECDHE-PSK-AES256-CBC-SHA",
    "ECDHE_PSK_WITH_AES_128_CBC_SHA256": "ECDHE-PSK-AES128-CBC-SHA256",
    "ECDHE_PSK_WITH_AES_256_CBC_SHA384": "ECDHE-PSK-AES256-CBC-SHA384",
    "ECDHE_PSK_WITH_NULL_SHA": "ECDHE-PSK-NULL-SHA",
    "ECDHE_PSK_WITH_NULL_SHA256": "ECDHE-PSK-NULL-SHA256",
    "ECDHE_PSK_WITH_NULL_SHA384": "ECDHE-PSK-NULL-SHA384",

    "PSK_WITH_CAMELLIA_128_CBC_SHA256": "PSK-CAMELLIA128-SHA256",
    "PSK_WITH_CAMELLIA_256_CBC_SHA384": "PSK-CAMELLIA256-SHA384",

    "DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256": "DHE-PSK-CAMELLIA128-SHA256",
    "DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384": "DHE-PSK-CAMELLIA256-SHA384",

    "RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256": "RSA-PSK-CAMELLIA128-SHA256",
    "RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384": "RSA-PSK-CAMELLIA256-SHA384",

    "ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256": "ECDHE-PSK-CAMELLIA128-SHA256",
    "ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384": "ECDHE-PSK-CAMELLIA256-SHA384",

    "PSK_WITH_AES_128_CCM": "PSK-AES128-CCM",
    "PSK_WITH_AES_256_CCM": "PSK-AES256-CCM",
    "DHE_PSK_WITH_AES_128_CCM": "DHE-PSK-AES128-CCM",
    "DHE_PSK_WITH_AES_256_CCM": "DHE-PSK-AES256-CCM",
    "PSK_WITH_AES_128_CCM_8": "PSK-AES128-CCM8",
    "PSK_WITH_AES_256_CCM_8": "PSK-AES256-CCM8",
    "DHE_PSK_WITH_AES_128_CCM_8": "DHE-PSK-AES128-CCM8",
    "DHE_PSK_WITH_AES_256_CCM_8": "DHE-PSK-AES256-CCM8",

    # ChaCha20-Poly1305 cipher suites, extending TLS v1.2
    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-RSA-CHACHA20-POLY1305",
    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-ECDSA-CHACHA20-POLY1305",
    "TLS_DHE_RSA_WITH_CHACHA20_POLY1305_SHA256": "DHE-RSA-CHACHA20-POLY1305",
    "TLS_PSK_WITH_CHACHA20_POLY1305_SHA256": "PSK-CHACHA20-POLY1305",
    "TLS_ECDHE_PSK_WITH_CHACHA20_POLY1305_SHA256": "ECDHE-PSK-CHACHA20-POLY1305",
    "TLS_DHE_PSK_WITH_CHACHA20_POLY1305_SHA256": "DHE-PSK-CHACHA20-POLY1305",
    "TLS_RSA_PSK_WITH_CHACHA20_POLY1305_SHA256": "RSA-PSK-CHACHA20-POLY1305"}

# TLS v1.3 cipher suites IANI to OpenSSL name translation
TLSV1_3_CIPHER_SUITES = {
    "TLS_AES_128_GCM_SHA256": "TLS_AES_128_GCM_SHA256",
    "TLS_AES_256_GCM_SHA384": "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256": "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_128_CCM_SHA256": "TLS_AES_128_CCM_SHA256",
    "TLS_AES_128_CCM_8_SHA256": "TLS_AES_128_CCM_8_SHA256"}

TLS_CIPHER_SUITES = {
    "TLSv1": TLSV1_CIPHER_SUITES,
    "TLSv1.1": TLSV1_1_CIPHER_SUITES,
    "TLSv1.2": TLSV1_2_CIPHER_SUITES,
    "TLSv1.3": TLSV1_3_CIPHER_SUITES}

OPENSSL_CS_NAMES = {
    "TLSv1": TLSV1_CIPHER_SUITES.values(),
    "TLSv1.1": TLSV1_1_CIPHER_SUITES.values(),
    "TLSv1.2": TLSV1_2_CIPHER_SUITES.values(),
    "TLSv1.3": TLSV1_3_CIPHER_SUITES.values()}
