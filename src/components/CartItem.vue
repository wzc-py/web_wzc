<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link to="/course/detail/1">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="expire" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option label="1个月有效" value="30" key="30"></el-option>
                <el-option label="2个月有效" value="60" key="60"></el-option>
                <el-option label="3个月有效" value="90" key="90"></el-option>
                <el-option label="永久有效" value="10000" key="10000"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{ course.price }}</div>
        <div class="cart_column column_4" @click="del_goods">删除</div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    data() {
        return {
            expire: "1个月有效",
        }
    },
    props: ['course'],
    watch: {
        // 监听selected是否发生了变化
        "course.selected": function () {
            this.change_selected();
        },
    },
    methods: {
        //查看用户是否登录
        check_login() {
            let token = sessionStorage.token;
            if (!token) {
                let self = this;
                this.$confirm("请先登录！", {
                    callback() {
                        self.$router.push("/login")
                    }
                })
                return false
            }
            return token
        },
        // 发起请求，修改redis中购物车的勾选状态
        change_selected() {
            let token = this.check_login();
            let course_id = this.course.id;
            let is_selected = this.course.selected;
            // console.log(course_id);
            // console.log(is_selected);
            this.$axios.put(this.$settings.HOST + "cartapp/option/", {
                course_id: course_id,
                is_selected: is_selected,
            }, {
                headers: {
                    // 购物车需要认证，写到token才能请求到后台
                    "Authorization": "jwt " + token
                }
            }).then(res => {
                this.$message("切换商品勾选状态成功");
            }).catch(error => {
                console.log("对不起，切换勾选状态失败！");
            })
        },
        //删除
        del_goods() {
            let token = this.check_login();
            this.$axios.delete(this.$settings.HOST + "cartapp/option/", {
                params: {
                    course_id: this.course.id,
                },
                headers: {
                    "Authorization": "jwt " + token,
                },
            }).then(response => {
                this.$message("删除成功！");
                this.$router.go(0);
            }).catch(error => {
                this.$message("删除失败！");
            })
        },
    },
    created() {
        this.check_login();
    }
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>
