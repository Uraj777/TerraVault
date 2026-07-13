document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.querySelector(".search-form input");
  const cards = document.querySelectorAll(".card");

  /
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    cards.forEach(card => {
      
      if (card.querySelector("h3")) {
        const title = card.querySelector("h3").textContent.toLowerCase();
        const text = card.querySelector("p").textContent.toLowerCase();
        
        card.style.display = title.includes(query) || text.includes(query) ? "flex" : "none";
      }
    });
  });

  
  const toggleBtn = document.createElement("button");
  if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.body.classList.add('dark-mode');
    toggleBtn.textContent = "☀️ Light Mode";
  } else {
    toggleBtn.textContent = "🌙 Dark Mode";
  }

  toggleBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 10px 15px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    background: var(--accent);
    color: white;
    font-size: 1rem;
    z-index: 1000;
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: background 0.3s;
  `;
  document.body.appendChild(toggleBtn);

  toggleBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    
   
    if (document.body.classList.contains("dark-mode")) {
      localStorage.setItem('theme', 'dark');
      toggleBtn.textContent = "☀️ Light Mode";
      toggleBtn.style.background = '#444'; 
    } else {
      localStorage.setItem('theme', 'light');
      toggleBtn.textContent = "🌙 Dark Mode";
      toggleBtn.style.background = 'var(--accent)';
    }
  });


  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-mode');
    toggleBtn.textContent = "☀️ Light Mode";
  }
});
