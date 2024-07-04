const tokenfield = document.getElementById("tokenfield")


const token = document.getElementById("token")

const validate = async () =>{

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    const response = await fetch("http://127.0.0.1:5002/login",
        {   method : "POST", 
            headers:{ "Content-Type":"application/json", }, body:JSON.stringify({username, password}) }
    )

    let data = await response.json()
    if (data["token"]){
        token.innerHTML = `Token: ${data["token"]}`
    }else{
        token.innerHTML = data["message"]
    }

}