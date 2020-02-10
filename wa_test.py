from twilio.rest import Client 
 
account_sid = 'AC74c51f7d88218337455c1aba6fb8e45c' 
auth_token = '1612839a4c29ad63b826eb534be2ad0a' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body='Your Yummy Cupcakes Company order of 1 dozen frosted cupcakes has shipped and should be delivered on July 10, 2019. Details: http://www.yummycupcakes.com/',      
                              to='whatsapp:+6289514845202' 
                          ) 
print(message.sid)