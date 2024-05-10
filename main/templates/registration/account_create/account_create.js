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
        human:false,                  
    }},

    methods:{
        //get current, last or next month

        create: function create(){
            if(!app.$data.human)
            {
            alert("Please confirm you are a person.");
            return;
            }

            app.$data.buttonText = '<i class="fas fa-spinner fa-spin"></i>';
            app.$data.loginErrorText = "";

            axios.post('{{request.path}}', {
                    action :"create",
                    formData : $("#create_form").serializeArray(), 
                                                
                })
                .then(function (response) {     
                    
                status=response.data.status;                               

                app.clearMainFormErrors();

                if(status == "error")
                {              
                    //form validation error           
                    app.displayErrors(response.data.errors);
                }
                else
                {
                    app.$data.status="done";
                }                        

                app.$data.buttonText = 'Submit <i class="fas fa-sign-in-alt"></i>';

                })
                .catch(function (error) {
                    console.log(error);                            
                });                        
        },

        showHelp:function showHelp(){                        
            $('#helpModal').modal('show');
        },

        humanChecker:function humanChecker(){
            app.$data.humanButtonText = 'Press if human <i class="fas fa-spinner fa-spin"></i>';
            setTimeout(app.humanConfirm, 1000); 
        },

        humanConfirm:function humanConfirm(){
            app.$data.humanButtonText = 'Thanks human <i class="fas fa-user-check"></i>';
            app.$data.human=true;
        },

        clearMainFormErrors:function clearMainFormErrors(){

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

                var elmnt = document.getElementById("div_id_" + e);
                elmnt.scrollIntoView(); 

            }
        },

        
    },            

    mounted(){
                                
    },
}).mount('#app');