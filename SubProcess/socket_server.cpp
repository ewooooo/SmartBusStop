#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <errno.h>

#include <iostream>

#define SA  struct sockaddr_in

using namespace std;
class Status{
    public:
    string status_0_EndCamera ="0";
    string status_1_ActivateCamera = "1";
    string status_2_BusWaiting = "2";
    string status_reset = "-1";
};
void insertString(char *result, int locate, string data){
    int len = data.length();
    for(int i = 0; i<len ; i++){
        result[locate+i] = data[i];
    }
}


int main()
{
    Status status = Status();
	const int port = 12345;

	int sock = socket(AF_INET, SOCK_STREAM, 0);
	int conn;

	SA addr, clientAddr;
	socklen_t len = sizeof(clientAddr);

	
	int send_len;
	int recv_len;

	addr.sin_family = AF_INET;
	addr.sin_port = htons(port);
	addr.sin_addr.s_addr = htonl(INADDR_ANY);

	if (bind(sock, (struct sockaddr*)&addr, sizeof(SA)) == -1) {
		fprintf(stderr, "Bind Error : %s\n", strerror(errno));
		close(sock);
		return(-1);
	}
	else printf("connected\n");

	if (listen(sock, 5) == -1) {
		printf("listen fail\n");
	}

	while (1) {

		conn = accept(sock, (struct sockaddr*)&clientAddr, &len);
        while(1){

            char buffer[10];
            ///////////////////////// recv ///////////////////////////////////
            while (recv_len = recv(conn, buffer, sizeof(buffer), 0) == -1) {
                if (errno == EINTR) {
                    continue;
                }
                else {
                    fprintf(stderr, "Recv Error : %s\n", strerror(errno));
                    return -1;
                }
            }
            ///////////////////////////////////////////////////////////////////
            
            for(int i = 0; i<strlen(buffer);i++){
                if(buffer[i] == '_'){
                    buffer[i] = '\0';
                }
            }

            cout<<buffer<<endl;
            
 
            string data(buffer); 
            strcpy(buffer,"_________");
            if (data == status.status_1_ActivateCamera || data == status.status_0_EndCamera){
                buffer[0] = status.status_1_ActivateCamera[0];
                buffer[1] = '|';
                string imageRetrunData;
                cin>>imageRetrunData;
                insertString(buffer, 2, imageRetrunData);

            }else if(data == status.status_2_BusWaiting){
                buffer[0] = status.status_2_BusWaiting[0];
                buffer[1] = '|';
                    //  버스 번호 발견 94551 발견못한 9455 버스 정
                    // [2, (0_버스 발견못함 1_버스 발견됨 2_버스 정차함 -1_대기 시간초과(버싀나감)), 버스번호]
                string imageRetrunData;
                cin>>imageRetrunData;

                if (imageRetrunData.length() == 4){
                    buffer[2] = '1';
                    buffer[3] = '|';
                    insertString(buffer, 4, imageRetrunData);
                }else if(imageRetrunData.length() == 5){
                    if (imageRetrunData[0] == '-'){
                        buffer[2] = '-';
                        buffer[3] = '1';
                        buffer[4] = '|';
                        insertString(buffer, 5, imageRetrunData.substr(imageRetrunData.length() - 4));
                    }else if(imageRetrunData[4] == '1'){
                        buffer[2] = '2';
                        buffer[3] = '|';
                        insertString(buffer, 4, imageRetrunData.substr(0,4));
                    }else{
                        buffer[2] = '0';
                    }
                }
                else if(imageRetrunData == "0"){
                    buffer[2] = '0';
                }

                else{
                    buffer[2] = '-';
                }

            }else if (data == status.status_reset){
                buffer[0] = status.status_reset[0];
            }

            cout<<buffer<<endl;
            cout<<sizeof(buffer)<<endl;
            ///////////////////////// Send ///////////////////////////////////
            while (send_len = send(conn, buffer, sizeof(buffer), 0) == -1) {
                if (errno == EINTR) {
                    continue;
                }
                else {
                    fprintf(stderr, "Send Error : %s\n", strerror(errno));
                    return -1;
                }
            }
            ///////////////////////////////////////////////////////////////////
        }
		close(conn);
	}
}