from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation emails.

    Behavior:
        - Inherits from Django's PasswordResetTokenGenerator.
        - Generates a unique token based on:
            1. The user's primary key (pk)
            2. A timestamp
            3. The user's is_active status
        - Changing is_active invalidates previous tokens automatically.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Constructs the hash value used to generate the token.

        Args:
            user (User): The Django user instance.
            timestamp (int): Timestamp in seconds.

        Returns:
            str: Concatenated string of user.pk, timestamp, and user.is_active.
        """
        return f"{user.pk}{timestamp}{user.is_active}"
account_activation_token = AccountActivationTokenGenerator()
