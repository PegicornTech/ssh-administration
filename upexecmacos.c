#include <libssh/libssh.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 6) {
        fprintf(stderr, "Usage: %s <host> <username> <password> <local_script> <remote_script>\n", argv[0]);
        return EXIT_FAILURE;
    }

    const char *host = argv[1];
    const char *username = argv[2];
    const char *password = argv[3];
    const char *local_script_path = argv[4];
    const char *remote_script_name = argv[5];

    ssh_session session = ssh_new();
    if (session == NULL) {
        fprintf(stderr, "Error initializing SSH session.\n");
        return EXIT_FAILURE;
    }

    ssh_options_set(session, SSH_OPTIONS_HOST, host);
    ssh_options_set(session, SSH_OPTIONS_USER, username);

    int rc = ssh_connect(session);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error connecting to %s: %s\n", host, ssh_get_error(session));
        ssh_free(session);
        return EXIT_FAILURE;
    }

    rc = ssh_userauth_password(session, NULL, password);
    if (rc != SSH_AUTH_SUCCESS) {
        fprintf(stderr, "Authentication failed: %s\n", ssh_get_error(session));
        ssh_disconnect(session);
        ssh_free(session);
        return EXIT_FAILURE;
    }

    ssh_channel channel = ssh_channel_new(session);
    if (channel == NULL) {
        fprintf(stderr, "Error creating SSH channel.\n");
        ssh_disconnect(session);
        ssh_free(session);
        return EXIT_FAILURE;
    }

    rc = ssh_channel_open_session(channel);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error opening channel session: %s\n", ssh_get_error(session));
        ssh_channel_free(channel);
        ssh_disconnect(session);
        ssh_free(session);
        return EXIT_FAILURE;
    }

    char command[512];
    snprintf(command, sizeof(command), "sudo -i && cp %s /home/%s/%s && chmod +x /home/%s/%s && nohup sh -c '/home/%s/%s' > script_output.log 2>&1 &",
             local_script_path, username, remote_script_name, username, remote_script_name, username, remote_script_name);

    rc = ssh_channel_request_exec(channel, command);
    if (rc != SSH_OK) {
        fprintf(stderr, "Error executing command: %s\n", ssh_get_error(session));
        ssh_channel_send_eof(channel);
        ssh_channel_close(channel);
        ssh_channel_free(channel);
        ssh_disconnect(session);
        ssh_free(session);
        return EXIT_FAILURE;
    }

    ssh_channel_send_eof(channel);
    ssh_channel_close(channel);
    ssh_channel_free(channel);
    ssh_disconnect(session);
    ssh_free(session);

    return EXIT_SUCCESS;
}

