axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ['[[', ']]'],
    
    data() {return {
        buttonText : 'Send <i class="fas fa-envelope"></i> ',
        messageText : "",
        form_ids : {{form_ids|safe}},         
        form_data : {{form_json|safe}},                 
    }},

    methods:{
        //get current, last or next month

        send_reset: function send_reset(){
            app.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            app.messageText = "";

            axios.post('{{request.path}}', {
                    action :"send_reset",
                    form_data : app.form_data, 
                                                
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
                    app.messageText = response.data.message;
                }
                else
                {
                    app.messageText = "Message sent to your email."
                }

                app.buttonText = '<i class="fas fa-envelope"></i> Send';

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