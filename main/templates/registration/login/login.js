

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ["[[", "]]"],

    data() { return {
        loginButtonText : 'Submit <i class="fas fa-sign-in-alt"></i>',
        loginErrorText : "",
        form_ids : {{form_ids|safe}},
        show_two_factor : false,
        two_factor_code : "",  
        show_two_factor_setup : false,    
        two_factor_uri : "",       
        two_factor_hash : "",   
        qr_code : null,     
        username:null,
        password:null,
        }                          
    },

    methods:{
        //get current, last or next month

        login:function login(){
            app.loginButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            app.loginErrorText = "";

            axios.post('/accounts/login/', {
                    action :"login",
                    form_data : {
                        username : app.username,
                        password : app.password,
                    }, 
                    two_factor_code : app.two_factor_code,
                                                
                })
                .then(function (response) {     
                    
                    status=response.data.status;                               

                    app.clear_main_form_errors();
      
                    if(status == "validation")
                    {              
                        //form validation error           
                        app.display_errors(response.data.errors);
                    }
                    else if(status == "error")
                    {
                        app.loginErrorText = response.data.message;
                    }
                    else if(status == "two_factor")
                    {
                        app.show_two_factor = true;
        
                        Vue.nextTick(() => {
                            document.getElementById("idtwofactorcode").focus();
                        });
                      
                    }
                    else if(status == "two_factor_setup")
                    {
                        app.show_two_factor = true;
                        app.show_two_factor_setup = true;
                        app.two_factor_uri = response.data.two_factor_uri;
                        app.two_factor_hash = response.data.two_factor_hash;
        
                        if(app.qr_code != null)
                        {
                        app.qr_code.clear();
                        app.qr_code.makeCode(app.two_factor_uri);
                        }
                        else
                        {
                        app.qr_code = new QRCode(document.getElementById("qrcode"), app.two_factor_uri);
                        }
                      
                    }
                    else
                    {
                        window.location = response.data.redirect_path;
                    }
      
                    app.loginButtonText = 'Submit <i class="fas fa-sign-in-alt"></i>';

                })
                .catch(function (error) {
                    console.log(error);                            
                });                        
        },

        clear_main_form_errors:function clear_main_form_errors(){
            for(let item in app.form_ids)
            {
                let e = document.getElementById("id_errors_" + app.form_ids[item]);
                if(e) e.remove();
            }
        },
        
        //display form errors
        display_errors: function display_errors(errors){
            for(let e in errors)
            {
                let str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(let i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';

                document.getElementById("div_id_" + e).insertAdjacentHTML('beforeend', str);

                document.getElementById("div_id_" + e).scrollIntoView();
                
            }
        },

        
    },            

    mounted() {
                                
    },
}).mount('#app');