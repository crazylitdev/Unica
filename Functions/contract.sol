pragma solidity ^0.8.7;

contract userDatabase {

    mapping(uint => User) public users;

    struct User {
        string _data;
    }

    function addPerson(uint _id, string memory _data) public {
        users[_id] = User(_data);
    }

    function GetUserInfo(uint _id) public view returns (string memory output) {
        return (users[_id]._data);
    }
}