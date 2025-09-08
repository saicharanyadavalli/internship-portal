document.addEventListener("DOMContentLoaded",()=>{
  const toggle=document.getElementById("themeToggle");
  toggle?.addEventListener("click",()=>{
    document.body.classList.toggle("theme-dark");
  });
});

