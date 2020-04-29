#include <iostream>
#include <algorithm>

using namespace std;


int main()
{
	
	 char inStr []= "4fd5 67 8";
	char num[] = { '0','1','2','3','4','5','6','7','8','9' };

	for (int i = 0; i<strlen(inStr); i++)
	{
		bool test = true;
		for (int j = 0; j < 10; j++) {
			if (inStr[i] == num[j]) {
				test = false;
			}
		}
		if (test) {
			inStr[i] = ' ';
		}

	}
	


	cout << inStr << endl;
	return 0;
}

