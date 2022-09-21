from ctypes.wintypes import DWORD
import pytest

import narrator.telegram.worker as w


def test_doc_worker_bytes_to_mib_str():
    trf = w.DocWorker._bytes_to_mib_str
    assert trf(0) == "0.00"
    assert trf(1) == "0.00"
    assert trf(23203) == "0.02"
    assert trf(925693) == "0.88"
    assert trf(2**20) == trf(2**20 - 1) == trf(2**20 + 1) == "1.00"
    assert trf(1234567890) == "1177.38"

    assert trf(925693, 5) == "0.88281"
    assert trf(925693, 1) == "0.9"
    assert trf(925693, 0) == "1"

    with pytest.raises(ValueError):
        _ = trf(925693, -1)
