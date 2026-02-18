const route = (event) => {
  console.log('event', event)
  event = event || window.event;
  event.preventDefault();
  window.history.pushState({}, event.target.href);
  handleLocation()
};

const routes = {
  404: "./pages/errors/page-not-found.html",
  '/401': "./pages/errors/page-not-authorized.html",
  '/500': "./pages/errors/page-something-wrong.html",
  '/offline': "./pages/errors/page-offline.html",
  '/notFound': "./pages/erros/page-search-not-found.html"
}

const handleLocation = async () => {
  const path = window.location.pathname;
  const route = routes[path] || routes[404];
  const html = await fetch(route).then(data => data.text());
  document.getElementById("main-page").innerHTML = html;
}

window.onpopstate = handleLocation;
window.route = route;

handleLocation();
