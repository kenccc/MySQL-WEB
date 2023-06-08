from prvniProject.main import GetHashedPass
import pytest 

def test_GetHashedPass():
    assert type(GetHashedPass("nwm")) == str

def test_GetHashedPass_Len():
    assert len(GetHashedPass("nwm")) == 128 

def test_GetHashedPass_doubleCheck():
    pass1 = GetHashedPass("nwm")
    pass2 = GetHashedPass("nwm")
    assert pass1 == pass2 

def test_Get_HashedPass_UnexpectedInputErr():
    with pytest.raises(AttributeError):
        GetHashedPass(64)