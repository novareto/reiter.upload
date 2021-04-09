import pytest
from reiter.upload.meta import StorageCenter
from reiter.upload.flat import FlatStorage
from reiter.upload.meta import FileInfo


def test_empty_store(test_file):
    center = StorageCenter()
    with pytest.raises(LookupError) as exc:
        center.store('somewhere', test_file)
    assert str(exc.value) == 'Namespace `somewhere` is unknown.'


def test_empty_retrieve():
    center = StorageCenter()
    with pytest.raises(LookupError) as exc:
        center.retrieve('somewhere', 'bogus_id')
    assert str(exc.value) == 'Namespace `somewhere` is unknown.'


def test_empty_get():
    center = StorageCenter()
    info = FileInfo(
        namespace='somewhere',
        ticket='12345678-1234-5678-1234-56781234567a',
        size=28,
        checksum=('md5', '53195454e1210adae36ecb34453a1f5a'),
        metadata={}
    )
    with pytest.raises(LookupError) as exc:
        center.get(info)
    assert str(exc.value) == 'Namespace `somewhere` is unknown.'


def test_register(tmp_path):
    center = StorageCenter()
    flat = FlatStorage('somewhere', tmp_path)
    center.register(flat)
    assert 'somewhere' in center.namespaces

    someother = FlatStorage('somewhere', tmp_path)
    with pytest.raises(NameError) as exc:
        center.register(someother)
    assert str(exc.value) == 'Namespace `somewhere` already exists.'


def test_store_get_retrieve(test_file, tmp_path):
    center = StorageCenter()
    flat = FlatStorage('somewhere', tmp_path)
    center.register(flat)
    info = center.store('somewhere', test_file)
    assert isinstance(info, FileInfo)