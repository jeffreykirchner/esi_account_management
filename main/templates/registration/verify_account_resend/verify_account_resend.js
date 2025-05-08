axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({
    delimiters: ['[[', ']]'],
      
    data() {return{
          
        emailVerified:true, 
        status:"update",  
        adminEmail : "",
        admainName : "",
        buttonText : 'Send Email Verification <i class="fas fa-envelope"></i>',
    }},

    methods:{
        //get list of users based on search
        sendVerificationEmail: function sendVerificationEmail(){
            
            app.buttonText = '<i class="fas fa-spinner fa-spin"></i>';

            axios.post("{%url 'verify-account-resend'%}", {                            
                action:"sendVerificationEmail",                             
            })
            .then(function (response) {                         
                app.status = response.data.status;
                app.buttonText ='Send Email Verification <i class="fas fa-envelope"></i>';
            })
            .catch(function (error) {
                console.log(error);                               
            }); 
        }, 

        getUser: function getUser(){
            axios.post("{%url 'verify-account-resend'%}", {                            
                action:"getUser",                                                            
            })
            .then(function (response) {                         
                app.emailVerified = response.data.emailVerified;
                app.adminEmail = response.data.adminEmail;
                app.admainName = response.data.admainName;
                // app.searchButtonText = 'Search <i class="fas fa-search"></i>';
            })
            .catch(function (error) {
                console.log(error);                               
            }); 
        }
        
    },
    
    mounted(){
        this.getUser();
    },
}).mount('#app');