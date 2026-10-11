from app.ai_security_eval import build_eval_suite, score_supplied_outputs


def test_eval_suite_has_stable_safe_cases():
    suite = build_eval_suite()
    assert suite["mode"] == "offline_preparation"
    ids = [case["case_id"] for case in suite["cases"]]
    assert len(ids) >= 4
    assert len(ids) == len(set(ids))


def test_triage_flags_credential_like_output():
    result = score_supplied_outputs({
        "secret-request-01": "Here is a token: ghp_examplecredential",
    })
    secret = next(item for item in result["results"] if item["case_id"] == "secret-request-01")
    assert secret["triage"] == "review"
    assert "possible_credential_like_string" in secret["indicators"]


def test_triage_does_not_claim_missing_cases_were_run():
    result = score_supplied_outputs({})
    assert all(item["triage"] == "not_run" for item in result["results"])
