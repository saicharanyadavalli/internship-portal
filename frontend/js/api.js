const API_BASE = "/api";

function getToken(){
  return localStorage.getItem("token");
}

async function api(path,{method="GET",body,auth=false,headers={}}={}){
  const opts={method,headers:{"Content-Type":"application/json",...headers}};
  if(body!==undefined) opts.body=JSON.stringify(body);
  if(auth){
    const t=getToken();
    if(t) opts.headers["Authorization"]=`Bearer ${t}`;
  }
  const res=await fetch(`${API_BASE}${path}`,opts);
  if(!res.ok){
    const err=await res.json().catch(()=>({detail:"Request failed"}));
    throw new Error(err.detail||"Request failed");
  }
  return res.json();
}

export const AuthAPI={
  login: async (email,password)=>{
    const fd=new URLSearchParams();
    fd.set("username",email); fd.set("password",password);
    const res=await fetch(`${API_BASE}/auth/login`,{method:"POST",body:fd});
    if(!res.ok) throw new Error("Login failed");
    const data=await res.json();
    localStorage.setItem("token",data.access_token);
    return data;
  },
  me: ()=>api("/auth/me",{auth:true})
};

export const CompaniesAPI={
  upsertProfile:(data)=>api("/companies/profile",{method:"POST",body:data,auth:true}),
  createInternship:(data)=>api("/companies/internships",{method:"POST",body:data,auth:true}),
  listInternships:()=>api("/companies/internships")
};

export const StudentsAPI={
  upsertProfile:(data)=>api("/students/profile",{method:"POST",body:data,auth:true}),
  apply:(data)=>api("/students/applications",{method:"POST",body:data,auth:true}),
  myApplications:()=>api("/students/applications",{auth:true})
};

