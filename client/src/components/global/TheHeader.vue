<template>
    <header class="wrapper">
        <div class="container container-pd52">
            <router-link to="/">
                <span class="logo">ENERGY//STAFF</span>
            </router-link>
            <div class="uauth-user-icon">
                <img src="../../assets/icons/Account.svg" width="48" height="48" alt="Личный кабинет">
            </div>
        </div>
    </header>
</template>

<style scoped>

.wrapper {
    background: #27282A;
    height: 80px;
    font-size: 16px;
    font-family: 'Montserrat';
}

.container {
    display: flex;
    align-items: center;
    height: 100%;
}

.logo {
    color: #FFFFFF;
    font-weight: 600;
}

.uauth-user-icon {
    margin-left: auto;
}

</style>
