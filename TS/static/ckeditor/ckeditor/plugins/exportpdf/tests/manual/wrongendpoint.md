<<<<<<< HEAD
@bender-tags: exportpdf, feature, 4
@bender-ui: collapsed
@bender-include: ../_helpers/tools.js
@bender-ckeditor-plugins: wysiwygarea, toolbar, notification

**Note:** Errors in console during this test are allowed.

1. Click `Export to PDF` button in the first editor.

  **Expected:**

  * Warning notification with `Error occured.` message appeared.
  * Button is clickable.
  * File wasn't downloaded.

  **Unexpected:**

  * Notification didn't show up.
  * Button wasn't reenabled.
  * File was downloaded.

2. Click `Export to PDF` button in the second editor.

  **Expected:**

  * Alert appeared instead of notification.
  * Button is clickable.
  * File wasn't downloaded.

  **Unexpected:**

  * Notification didn't show up.
  * Button wasn't reenabled.
  * File was downloaded.
=======
@bender-tags: exportpdf, feature, 4
@bender-ui: collapsed
@bender-include: ../_helpers/tools.js
@bender-ckeditor-plugins: wysiwygarea, toolbar, notification

**Note:** Errors in console during this test are allowed.

1. Click `Export to PDF` button in the first editor.

  **Expected:**

  * Warning notification with `Error occured.` message appeared.
  * Button is clickable.
  * File wasn't downloaded.

  **Unexpected:**

  * Notification didn't show up.
  * Button wasn't reenabled.
  * File was downloaded.

2. Click `Export to PDF` button in the second editor.

  **Expected:**

  * Alert appeared instead of notification.
  * Button is clickable.
  * File wasn't downloaded.

  **Unexpected:**

  * Notification didn't show up.
  * Button wasn't reenabled.
  * File was downloaded.
>>>>>>> ffd1ae02a8e9800d077d03490e0e33d88fcb9928
