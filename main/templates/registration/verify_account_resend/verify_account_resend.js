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
            
            app.$data.buttonText = '<i class="fas fa-spinner fa-spin"></i>';

            axios.post("{%url 'verify-account-resend'%}", {                            
                action:"sendVerificationEmail",                             
            })
            .then(function (response) {                         
                app.$data.status = response.data.status;
                app.$data.buttonText ='Send Email Verification <i class="fas fa-envelope"></i>';
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
                app.$data.emailVerified = response.data.emailVerified;
                app.$data.adminEmail = response.data.adminEmail;
                app.$data.admainName = response.data.admainName;
                // app.$data.searchButtonText = 'Search <i class="fas fa-search"></i>';
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