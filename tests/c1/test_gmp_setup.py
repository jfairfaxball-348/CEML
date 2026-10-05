"""Stage: hardware characterization; archive and PE inspection regression checks."""
import io
from pathlib import Path
import struct
import sys
import tarfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/c1'))
import gmp_setup as setup


def archive_member(name, kind=tarfile.REGTYPE):
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode='w') as archive:
        member = tarfile.TarInfo(name)
        member.type = kind
        member.size = 1 if kind == tarfile.REGTYPE else 0
        archive.addfile(member, io.BytesIO(b'x') if member.size else None)
    return output.getvalue()


class ArchiveChecks(unittest.TestCase):
    def test_regular_member(self):
        self.assertEqual(setup.inspect_tar(archive_member('ucrt64/include/gmp.h')),
                         {'ucrt64/include/gmp.h': b'x'})

    def test_unsafe_components_and_links(self):
        separator = chr(47)
        for name in (separator.join(('..', 'escape')), separator.join(('ucrt64', '..', '..', 'escape')), 'gmp.h:alternate', 'one\\two'):
            with self.subTest(name=name), self.assertRaises(setup.Refusal):
                setup.inspect_tar(archive_member(name))
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE):
            with self.subTest(kind=kind), self.assertRaises(setup.Refusal):
                setup.inspect_tar(archive_member('gmp.h', kind))

    def test_duplicate_member(self):
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode='w') as archive:
            for _ in range(2):
                member = tarfile.TarInfo('gmp.h')
                archive.addfile(member)
        with self.assertRaises(setup.Refusal):
            setup.inspect_tar(output.getvalue())

    def test_cumulative_bound(self):
        old = setup.EXTRACT_LIMIT
        try:
            setup.EXTRACT_LIMIT = 0
            with self.assertRaises(setup.Refusal):
                setup.inspect_tar(archive_member('gmp.h'))
        finally:
            setup.EXTRACT_LIMIT = old


class PEChecks(unittest.TestCase):
    def test_bad_target_and_truncation(self):
        for data in (b'', b'MZ', b'MZ'+b'\0'*100):
            with self.subTest(length=len(data)), self.assertRaises(setup.Refusal):
                setup.pe_info(data)

    def test_uninitialized_data_export_is_data(self):
        # A data export can reside in a zero-initialized section with no raw bytes.
        data = bytearray(1024)
        data[:2] = b'MZ'
        struct.pack_into('<I', data, 60, 128)
        data[128:132] = b'PE\0\0'
        struct.pack_into('<HH', data, 132, 0x8664, 2)
        struct.pack_into('<H', data, 148, 240)
        struct.pack_into('<H', data, 152, 0x20b)
        struct.pack_into('<IIII', data, 264, 4096, 120, 0, 0)
        struct.pack_into('<IIII', data, 400, 512, 4096, 512, 512)
        struct.pack_into('<I', data, 428, 0x40000040)
        struct.pack_into('<IIII', data, 440, 512, 8192, 0, 0)
        struct.pack_into('<I', data, 468, 0xC0000080)
        struct.pack_into('<IIIII', data, 532, 1, 1, 4144, 4148, 4152)
        struct.pack_into('<I', data, 560, 8192)
        struct.pack_into('<I', data, 564, 4160)
        struct.pack_into('<H', data, 568, 0)
        data[576:591] = b'__gmp_version\0\0'
        info = setup.pe_info(bytes(data))
        self.assertEqual(info['exports'], {'__gmp_version': 'data'})


if __name__ == '__main__':
    unittest.main()
