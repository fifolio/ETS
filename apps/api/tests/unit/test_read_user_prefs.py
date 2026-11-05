from app.services.appwrite.read_user_prefs import read_user_prefs


class WithData:
    data = {"role": "Nurse"}


class WithModelDump:
    def model_dump(self):
        return {"role": "Doctor"}


def test_returns_a_plain_dict_as_it_is():
    assert read_user_prefs({"role": "Architect"}) == {"role": "Architect"}


def test_reads_a_data_attribute():
    assert read_user_prefs(WithData()) == {"role": "Nurse"}


def test_falls_back_to_model_dump():
    assert read_user_prefs(WithModelDump()) == {"role": "Doctor"}


def test_returns_an_empty_dict_for_anything_else():
    assert read_user_prefs(object()) == {}
