import chromadb


def chroma_connect():
    try:
        return chromadb.HttpClient(
            host='127.0.0.1',
            port=5454,
            settings=chromadb.Settings(
                anonymized_telemetry=False,
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials='fZ8v2nLg93sdxP1qkB7wma49e',
            ),
        )
    except ValueError as ex:
        raise ex
