axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({

    delimiters: ['[[', ']]'],
    
    data() {return{
        buttonText : '<i class="fas fa-user-edit"></i> Update',
        form_ids : {{form_ids|safe}},    
        status: "update", 
        email_verification_required: false,                  
    }},

    methods:{
        //get current, last or next month

        update(){

            app.$data.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            
            axios.post('{{request.path}}', {
                    action :"update",
                    formData : $("#updateForm").serializeArray(),                              
                })
                .then(function (response) {     
                    
                status = response.data.status;                               

                app.clearMainFormErrors();

                if(status == "error")
                {              
                    //form validation error           
                    app.displayErrors(response.data.errors);
                }
                else
                {
                    app.$data.status = "done";
                    app.$data.emailVerificationRequired = response.data.email_verification_required;
                }                        

                app.$data.buttonText = 'Update <i class="fas fa-sign-in-alt"></i>';

                })
                .catch(function (error) {
                    console.log(error);                            
                });                        
            },

            clearMainFormErrors(){

                s = app.$data.form_ids;                    
                for(var i in s)
                {
                    $("#id_" + s[i]).attr("class","form-control");
                    $("#id_errors_" + s[i]).remove();
                }

            },
        
        //display form errors
        displayErrors(errors){
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

                    var elmnt = document.getElementById("div_id_" + e);
                    elmnt.scrollIntoView(); 

                }
            },

        
    },            

    mounted(){
                                
    },
}).mount('#app');