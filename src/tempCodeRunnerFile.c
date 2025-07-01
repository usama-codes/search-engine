#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MSG_SIZE 50

int main() {
    int pipe1[2], pipe2[2];
    pid_t pid;
    char parent_msg[] = "Hello Child Process";
    char child_msg[] = "Hi Parent Process";
    char buffer[MSG_SIZE];

    // Create the first pipe (parent -> child)
    if (pipe(pipe1) == -1) {
        perror("Pipe1 failed");
        exit(EXIT_FAILURE);
    }
    
    // Create the second pipe (child -> parent)
    if (pipe(pipe2) == -1) {
        perror("Pipe2 failed");
        exit(EXIT_FAILURE);
    }
    
    pid = fork();
    
    if (pid < 0) {
        perror("Fork failed");
        exit(EXIT_FAILURE);
    }
    
    if (pid == 0) { // Child process
        close(pipe1[1]); // Close unused write end of pipe1
        close(pipe2[0]); // Close unused read end of pipe2
        
        // Read message from parent
        read(pipe1[0], buffer, MSG_SIZE);
        printf("Child received: %s\n", buffer);
        
        // Send response to parent
        write(pipe2[1], child_msg, strlen(child_msg) + 1);
        
        close(pipe1[0]);
        close(pipe2[1]);
    } else { // Parent process
        close(pipe1[0]); // Close unused read end of pipe1
        close(pipe2[1]); // Close unused write end of pipe2
        
        // Send message to child
        write(pipe1[1], parent_msg, strlen(parent_msg) + 1);
        
        // Read response from child
        read(pipe2[0], buffer, MSG_SIZE);
        printf("Parent received: %s\n", buffer);
        
        close(pipe1[1]);
        close(pipe2[0]);
    }
    
    return 0;
}
