axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ['[[', ']]'],
    
    data() {return {
        buttonText : 'Send <i class="fas fa-envelope"></i> ',
        messageText : "",
        form_ids : {{form_ids|safe}},                          
    }},

    methods:{
        //get current, last or next month

        send_reset: function send_reset(){
            app.$data.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            app.$data.messageText = "";

            axios.post('{{request.path}}', {
                    action :"send_reset",
                    form_data : $("#password_reset_form").serializeArray(), 
                                                
                })
                .then(function (response) {     
                    
                status=response.data.status;                               

                app.clearMainFormErrors();

                if(status == "validation")
                {              
                    //form validation error           
                    app.displayErrors(response.data.errors);
                }
                else if(status == "error")
                {
                    app.$data.messageText = response.data.message;
                }
                else
                {
                    app.$data.messageText = "Message sent to your email."
                }

                app.$data.buttonText = '<i class="fas fa-envelope"></i> Send';

                })
                .catch(function (error) {
                    console.log(error);                            
                });                        
        },

        clearMainFormErrors: function clearMainFormErrors(){

            s = app.$data.form_ids;                    
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }

        },
        
        //display form errors
        displayErrors: function displayErrors(errors){
            for(var e in errors)
            {
                $("#id_" + e).attr("class","form-control is-invalid")
                var str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(var i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';
                $("#div_id_" + e).append(str); 

            }
        },

        
    },            

    mounted(){
                                
    },
}).mount('#app');