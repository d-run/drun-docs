---
hide:
  - toc
---

# App Dialogue Instructions

**Dialogue** is the most common way to obtain information since the emergence of ChatGPT. In d.run, once an app is published, the dialogue function can be used. You can freely ask questions in the dialogue after linking to a corpus, consult historical records at any time, and the navigation bar also lists the recently used dialogues.

## Daily Dialogue

### RAG App

1. In the left navigation bar, click on **App Center**, select the published RAG type app, and click the dialogue icon in the lower right corner.

    <!-- ![Click dialogue icon](../../images/chat01.jpg) -->

2. Enter your question in the dialogue box, click **Send**, or press the Enter key to start the conversation.

    <!-- ![Chat](../../images/chat02.jpg) -->

### Full Text Reading App

1. In the left navigation bar, click on **App Center**, select the published **Full Text Reading** type app, and click the dialogue icon in the lower right corner.

    <!-- ![Click dialogue icon](../../images/chat03.jpg) -->

2. Upload a file in the lower right corner of the dialogue box and ask questions based on the content of the file. Click **Send**, or press the Enter key to start the conversation.

    <!-- ![Chat](../../images/chat04.jpg) -->

### Combination App

1. In the left navigation bar, click on **App Center**, select the published **Combination App** type app, and click the dialogue icon in the lower right corner.

    <!-- ![Click dialogue icon](../../images/chat05.jpg) -->

2. Enter your question in the dialogue box, click **Send**, or press the Enter key to start the conversation.

    <!-- ![Chat](../../images/chat06.jpg) -->

## Dialogue Management

<!-- ![manage](../images/manage.jpg) -->

- **Pin**, **Rename**, and **Delete**: In the history pane, click the **┇** on the right side of a dialogue to pin, rename, or delete the dialogue.
- **Clear**: In the upper left corner of the dialogue page, click the 🧹 icon to **clear** the dialogue.
- **Link Corpus**: In the lower left corner of the input box, click the 📖 icon to link the corpus.

    Selection of corpus: The **chat app** will match the most similar corpus in the selected corpus as a reference to answer your questions. A successful operation will indicate that the corpus has been selected. You can also deselect one or more corpora.

    !!! info

        If you cannot select or change the linked corpus, you can only add a corpus. The vectorization model of the app must be consistent with the vectorization model of the corpus to be usable.

- **Stop Dialogue**: After asking a question, click the icon on the right side of the input box to stop the dialogue, allowing the assistant to cease outputting content.

## Some Useful Icons

<!-- ![page-function](../images/page-function.jpg) -->

- **Rating**: You can like 👍 or dislike 👎 a response, depending on your satisfaction with the content of the answer.
- **Copy**: You can copy a response.
- **Reset**: You can reset or regenerate a specific response.

    !!! info "Randomness"

        For the reset content, the administrator can adjust the model's **randomness** to control the consistency of the assistant's responses over multiple attempts.

        If the randomness is high, the assistant's responses may vary each time. If high accuracy is required, the randomness can be lowered, resulting in more consistent outputs from the assistant each time.

- **Delete**: Click the trash can :material-delete: icon to delete a response, after which the deleted dialogue will not be remembered in the context of the assistant's conversation.
- **Feedback**: Click the last icon :bookmark_tabs: of a response to submit feedback, providing comments based on the quality of the assistant's responses.
