<template>
    <div class="footer">
        <ul>
            <li v-for="(footer,key) in footer_list" :key="key">
                <span v-if="footer.is_site"><a :href="footer.link">{{ footer.title }}</a></span>
                <span v-else><router-link :to="footer.link">{{ footer.title }}</router-link></span>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "Footer",
        data() {
            return {
                footer_list: [],
            }
        },
        methods: {
            get_footer() {
                this.$axios({
                    url: this.$settings.HOST + "homeapp/footer/",
                    method: 'get'
                }).then(res => {
                    // console.log(res);
                    this.footer_list = res.data;
                }).catch(error => {
                    console.log(error);
                })
            },
            fly(link) {
                this.$router.push('link')
            }
        },
        created() {
            this.get_footer();
        },
    }
</script>

<style scoped>
    .footer {
        width: 100%;
        height: 128px;
        background: #fff;
        color: #fff;
    }

    .footer ul {
        margin: 0 auto 16px;
        padding-top: 38px;
        width: 810px;
    }

    .footer ul li {
        float: left;
        width: 112px;
        margin: 0 10px;
        text-align: center;
        font-size: 14px;
    }

    .footer ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .footer p {
        text-align: center;
        font-size: 12px;
    }
</style>
