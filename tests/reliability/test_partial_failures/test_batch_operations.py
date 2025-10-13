"""Tests for batch operation error handling."""


def test_batch_operation_collects_errors():
    """Batch operation collects all errors without stopping."""
    def process_batch(items, processor):
        """Process batch and collect errors."""
        results = []
        errors = []

        for item in items:
            try:
                result = processor(item)
                results.append(result)
            except Exception as e:
                errors.append({'item': item, 'error': str(e)})

        return results, errors

    def processor(item):
        """Sample processor that fails on even numbers."""
        if item % 2 == 0:
            raise Exception(f"Failed on {item}")
        return item * 2

    items = [1, 2, 3, 4, 5]
    results, errors = process_batch(items, processor)

    assert results == [2, 6, 10]  # Odd numbers processed
    assert len(errors) == 2  # Even numbers failed
