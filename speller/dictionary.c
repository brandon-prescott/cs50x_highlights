// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

int dict_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{

    int hash_index = 0;

    node *search;

    hash_index = hash(word);

    // If linked list for this hash index is empty return false
    if (table[hash_index] == NULL)
    {
        return false;
    }

    // Set search pointer to point to the same node as the head of the linked list
    search = table[hash_index];

    // While the search pointer has not reached the end of the list
    while (search != NULL)
    {
        // Compare the input word against the current node
        // Return true if they match
        if (strcasecmp(search->word, word) == 0)
        {
            return true;
        }
        // Else search the next node
        else
        {
            search = search->next;
        }
    }

    // Return false if the end of the list is reached without finding a match
    return false;
}

// Hashes word to a number
// Uses the first two characters to assign an index i.e. aa = 0, ab = 1, ac = 2...
unsigned int hash(const char *word)
{
    unsigned int first_character = 0;
    unsigned int second_character = 0;
    unsigned int hash = 0;

    // First character is multiples of 26
    first_character = (toupper(word[0]) - 'A') * 26;

    // If the second character is NULL, just set it to 0
    if (toupper(word[1]) == 0)
    {
        second_character = 0;
    }
    // Else assign it as a number between 0 and 25
    else
    {
        second_character = (toupper(word[1]) - 'A');
    }

    // Sum the two values together to obtain hash code
    hash = first_character + second_character;

    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    unsigned int hash_index = 0;
    int index = 0;
    char word[LENGTH + 1];

    // Opens dictionary file
    FILE *inp_dict = fopen(dictionary, "r");
    // Returns error if cannot load dictionary file
    if (inp_dict == NULL)
    {
        printf("Could not load dictionary.\n");
        return false;
    }

    char c;
    // Loop through each character in dictionary and read it to buffer
    while (fread(&c, sizeof(char), 1, inp_dict))
    {
        // If the character is alphabetical or an apostrophe
        if (isalpha(c) || (c == '\'' && index > 0))
        {
            // Append the character to the current word array and increment character index
            word[index] = c;
            index++;
        }
        else
        {
            // Close off word with null character and increase word count
            word[index] = '\0';
            dict_words++;

            // Get hash index for current word
            hash_index = hash(word);

            // Pointer for traversing the linked list
            node *trav;

            // Allocate memory for a new node
            node *n = malloc(sizeof(node));
            if (n == NULL)
            {
                return false;
            }

            // For each character in the current word array
            for (int i = 0; i <= index; i++)
            {
                // Append each character to the word field in the current node
                n->word[i] = word[i];
            }
            // Point the new node to NULL to indicate it is the new end of the list
            n->next = NULL;

            // If linked list is empty, point the head of the list to the newly created node
            if (table[hash_index] == NULL)
            {
                table[hash_index] = n;
            }
            else
            {
                // Assign travel pointer to point to the first node in the list
                trav = table[hash_index];

                // Whilst the travel pointer is not pointing to NULL (end of list)
                while (trav->next != NULL)
                {
                    // Update travel pointer to point to the next node
                    trav = trav->next;
                }
                // Once the end of the list is reached, get the last node to point to the newly created node, extending the list
                trav->next = n;

            }

            // Reset character index
            index = 0;

        }
    }

    fclose(inp_dict);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return dict_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    int words_freed = 0;
    node *list;

    // For each list in the has table
    for (int i = 0; i < N; i++)
    {
        // Set list pointer to point to the first node in the hash index
        list = table[i];

        // While the end of the list has not been reached
        while (list != NULL)
        {
            // Create a temporary node that is one step ahead of list
            node *tmp = list->next;

            // Free the node that list is pointing to
            free(list);

            // Set list to point to the next node via tmp
            list = tmp;

            words_freed++;
        }

    }

    // If the total number of words freed matches the number of words in the dictionary, the function has ran successfully
    if (words_freed == dict_words)
    {
        return true;
    }
    else
    {
        return false;
    }

}
