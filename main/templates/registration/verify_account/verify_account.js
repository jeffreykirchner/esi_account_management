axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = Vue.createApp({
    delimiters: ['[[', ']]'],
      
    data() {return {

        emailVerified:{%if emailVerified%}true{%else%}false{%endif%},
        failed:{%if failed%}true{%else%}false{%endif%},
        status:"update",  
        adminEmail : "",
        admainName : "",
        buttonText : 'Click to Verify <i class="fas fa-sign-in-alt"></i>',
    }},

    methods:{
        //get list of users based on search
        verifyEmail(){
            
            app.$data.buttonText = '<i class="fas fa-spinner fa-spin"></i>';

            axios.post('{{request.path}}', {                            
                action:"verifyEmail",                             
            })
            .then(function (response) {                         
                app.$data.emailVerified = response.data.emailVerified;
                app.$data.failed = response.data.failed;
                app.$data.buttonText ='Click to Verify <i class="fas fa-sign-in-alt"></i>';
            })
            .catch(function (error) {
                console.log(error);                               
            }); 
        }, 
        
    },
    
    mounted(){
        
    },
}).mount('#app');