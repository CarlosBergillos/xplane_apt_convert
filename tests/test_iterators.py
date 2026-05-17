import pytest

from xplane_apt_convert.iterators import BIterator


class TestBIterator:
    def test_iterates_all_elements(self):
        result = list(BIterator([1, 2, 3]))
        assert result == [1, 2, 3]

    def test_empty_sequence(self):
        assert list(BIterator([])) == []

    def test_has_next_true_at_start(self):
        it = BIterator([1, 2])
        next(it)
        assert it.has_next()

    def test_has_next_false_at_end(self):
        it = BIterator([1])
        next(it)
        assert not it.has_next()

    def test_has_next_false_on_empty(self):
        it = BIterator([])
        assert not it.has_next()

    def test_unnext_allows_rereading(self):
        it = BIterator([1, 2, 3])
        first = next(it)
        it.unnext()
        reread = next(it)
        assert first == reread == 1

    def test_unnext_at_initial_position_raises(self):
        it = BIterator([1, 2])
        with pytest.raises(IndexError):
            it.unnext()

    def test_stop_iteration_at_end(self):
        it = BIterator([1])
        next(it)
        with pytest.raises(StopIteration):
            next(it)
