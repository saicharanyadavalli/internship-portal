document.addEventListener("DOMContentLoaded",function(){
  const form=document.getElementById("loginForm");
  if(!form) return;
  form.addEventListener("submit",async function(e){
    e.preventDefault();
    const username=document.getElementById("username")?.value.trim()||"";
    const password=document.getElementById("password")?.value.trim()||"";
    if(!username||!password){
      alert("Please enter email and password.");
      return;
    }
    const body=new URLSearchParams();
    body.set("username",username);
    body.set("password",password);
    try{
      const res=await fetch("/api/auth/login",{
        method:"POST",
        headers:{"Content-Type":"application/x-www-form-urlencoded"},
        body:body.toString()
      });
      const data=await res.json().catch(()=>null);
      if(res.ok&&data?.access_token){
        localStorage.setItem("token",data.access_token);
        window.location.href="dashboard.html";
      }else{
        const msg=(data&&(data.detail||data.message))||"Invalid credentials.";
        alert(`Error: ${msg}`);
      }
    }catch(err){
      console.error(err);
      alert("Failed to connect to server.");
    }
  });
});

