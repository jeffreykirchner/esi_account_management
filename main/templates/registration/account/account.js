axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ['[[', ']]'],
    
    data() {return{
        buttonText : 'Update <i class="fas fa-user-edit"></i>',
        form_ids : {{form_ids|safe}},    
        form_data : {{form_json|safe}},
        status: "update", 
        email_verification_required: false,                  
    }},

    methods:{
        //get current, last or next month

        update: function update(){

            app.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            
            axios.post('{{request.path}}', {
                    action :"update",
                    form_data : app.form_data,                              
                })
                .then(function (response) {     
                    
                status = response.data.status;                               

                app.clear_main_form_errors();

                if(status == "error")
                {              
                    //form validation error           
                    app.display_errors(response.data.errors);
                }
                else
                {
                    app.status = "done";
                    app.email_verification_required = response.data.email_verification_required;
                }                        

                app.buttonText = 'Update <i class="fas fa-sign-in-alt"></i>';

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

    mounted(){
                                
    },
}).mount('#app');