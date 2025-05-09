axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({
    delimiters: ["[[", "]]"],
      
    data() {return {
        buttonText : 'Submit <i class="fas fa-sign-in-alt"></i>',
        humanButtonText : 'Press if human <i class="far fa-user-circle"></i>',
        loginErrorText : "",
        form_ids : {{form_ids|safe}},    
        status:"update", 
        form_data : {{form_json|safe}},
        human:false,                  
    }},

    methods:{
        //get current, last or next month

        create: function create(){
            if(!app.human)
            {
            alert("Please confirm you are a person.");
            return;
            }

            app.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            app.loginErrorText = "";

            axios.post('{{request.path}}', {
                    action :"create",
                    form_data : app.form_data, 
                                                
                })
                .then(function (response) {     
                    
                status=response.data.status;                               

                app.clear_main_form_errors();

                if(status == "error")
                {              
                    //form validation error           
                    app.display_errors(response.data.errors);
                }
                else
                {
                    app.status="done";
                }                        

                app.buttonText = 'Submit <i class="fas fa-sign-in-alt"></i>';

                })
                .catch(function (error) {
                    console.log(error);                            
                });                        
        },

        humanChecker:function humanChecker(){
            app.humanButtonText = 'Press if human <i class="fas fa-spinner fa-spin"></i>';
            setTimeout(app.humanConfirm, 1000); 
        },

        humanConfirm:function humanConfirm(){
            app.humanButtonText = 'Thanks human <i class="fas fa-user-check"></i>';
            app.human=true;
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

    mounted(){
                                
    },
}).mount('#app');