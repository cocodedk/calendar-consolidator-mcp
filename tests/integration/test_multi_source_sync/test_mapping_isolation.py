"""Tests for separate mapping isolation per source."""


def test_multi_source_maintains_separate_mappings(mock_config_multi_source):
    """Each source maintains separate event mappings."""
    from python.sync.syncer import Syncer

    mock_config_multi_source.sources.get.side_effect = [
        {'id': 1, 'calendar_id': 'source1'},
        {'id': 2, 'calendar_id': 'source2'}
    ]

    mock_config_multi_source.mappings.get_all_for_source.side_effect = [
        [{'source_event_uid': 'evt1', 'target_event_id': 'tgt1', 'source_id': 1}],
        [{'source_event_uid': 'evt2', 'target_event_id': 'tgt2', 'source_id': 2}]
    ]

    syncer = Syncer(mock_config_multi_source)

    # Get mappings for each source
    mappings1 = mock_config_multi_source.mappings.get_all_for_source(1)
    mappings2 = mock_config_multi_source.mappings.get_all_for_source(2)

    # Mappings should be separate
    assert len(mappings1) == 1
    assert len(mappings2) == 1
    assert mappings1[0]['source_id'] != mappings2[0]['source_id']
