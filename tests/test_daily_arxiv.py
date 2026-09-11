import arxiv

import daily_arxiv


def test_fetch_arxiv_results_uses_capped_page_size(monkeypatch):
    result = object()
    calls = []

    class Client:
        def __init__(self, page_size, delay_seconds, num_retries):
            calls.append((page_size, delay_seconds, num_retries))

        def results(self, search_engine):
            return iter([result])

    monkeypatch.setattr(daily_arxiv.arxiv, "Client", Client)

    assert daily_arxiv.fetch_arxiv_results(object(), 50, "topic") == [result]
    assert calls == [(20, 10.0, 2)]


def test_fetch_arxiv_results_preserves_existing_papers_on_arxiv_error(monkeypatch):
    calls = []

    class Client:
        def __init__(self, page_size, delay_seconds, num_retries):
            calls.append((page_size, delay_seconds, num_retries))

        def results(self, search_engine):
            raise arxiv.ArxivError("url", 0, "failed")

    monkeypatch.setattr(daily_arxiv.arxiv, "Client", Client)
    monkeypatch.setattr(daily_arxiv, "arxiv_retry_delays", ())

    assert daily_arxiv.fetch_arxiv_results(object(), 50, "topic") == []
    assert calls == [(20, 10.0, 2)]
