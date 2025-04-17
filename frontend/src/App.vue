<template>
  <div id="app">
    <header>
      <div class="header-content">
        <img src="@/assets/logo.png" alt="Clarkson Hockey Logo" class="logo" />
        <div class="header-text">
          <h1>Women's Hockey Recruitment Database</h1>
        </div>
      </div>
      <div class="divider"></div>
      <nav>
        <h2>
          <router-link router-link to="/players">Players</router-link>
          <router-link to="/games">Games</router-link>
        </h2>
      </nav>
    </header>
    <main> 
      <router-view /> <!-- Content for each page will be rendered here -->
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<!-- color: #fff;
  font-family: "Montserrat";
  font-size: 16px;
  font-weight: 600;
  font-style: normal;
  letter-spacing: 3.2px;
  line-height: 24px;
  text-align: left;
  text-transform: uppercase; -->

<style>
#app {
  font-family: Arial, sans-serif;
  text-align: center;
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  background-color: #cfd0d1;
}

header {
  background-color: #004e42;
  width: 100%;
  color: #fff;
  padding: 10px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000; /* Ensure the header is above other content */
  box-sizing: border-box; /* Include padding in width/height calculations */
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%; /* Ensure the content spans the full width */
}

.logo {
  width: 150px;
  height: 50px;
  margin-left: 30px;
  margin-right: 20px;
}

.header-text {
  flex: 1; /* Allow the header text to take up remaining space */
  text-align: left; /* Align the text to the left */
}

.divider {
  width: 100%;
  height: 1.5px;
  background-color: #ffcd00;
  margin: 10px 0; /* Add some space above and below the divider */
}

h1 {
  margin: 10px; /* Remove any default margin */
  margin-top: 25px;
  margin-bottom: 25px;
  font-family: 'Montserrat', sans-serif;
  color: #fff;
  font-size: 1.15rem;
  font-weight: 600;
  font-style: normal;
  letter-spacing: 3.04px;
  line-height: 24px;
  text-transform: uppercase;
}

h2 {
  font-family: 'Montserrat', sans-serif;
  font-size: .8rem;
  font-weight: 600;
  font-style: normal;
  letter-spacing: 3.04px;
  line-height: 24px;
  text-align: left;
  text-transform: uppercase;
  flex-direction: row;
  margin: 0;
}

main {
  margin-top: 140px; /* Push the content below the fixed header */
  padding: 20px;
  box-sizing: border-box;
  width: 100%;
}

nav {
  display: flex;
  justify-content: center;
}

nav a {
  color: white;
  margin: 0 100px;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

/* Reset body and html styles */
body, html {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden; /* Prevent horizontal scrolling */
}

</style>