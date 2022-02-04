import React, {useState, useEffect} from 'react';
import axios from 'axios';

function Home({auth}) {

    const [name, setName] = useState(null);
    const [userInfo, setInfo] = useState({
        first_name: "",
        id: 0,
        last_name: "",
        phone_number: "",
        time: 0,
        username: ""
    });

  useEffect(() => {
    const username = localStorage.getItem("user");
    setName(username);
    console.log(username);
    axios.get(`http://localhost:8000/users/?uname=${username}`)
        .then(response => {
            console.log(response.data.data);
            setInfo(response.data.data)
        })
        .catch(error => {
            console.log(error);
        });

}, []);


  return <div>
      {auth &&
        <div>Hello {userInfo.first_name} {userInfo.last_name}! <br/> Phone No: {userInfo.phone_number}
        <br/> Time: {userInfo.time} minutes
        </div>
        
      }
      {!auth &&
        <div>Please login</div>
      }

  </div>;
}

export default Home;
