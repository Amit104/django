#include<stdio.h>
#include<stdlib.h>

struct node
{
    int val;
    struct node* next;
};

struct node* create(int value)
{
    struct node* temp=(struct node*)malloc(sizeof(struct node));
    temp->val=value;
    temp->next=NULL;
    return temp;
}

int main()
{
    struct node *temp1,*temp2,*head,*A,*B;

    A=create(5);
    A->next=create(8);
    A->next->next=create(20);

    B=create(4);
    B->next=create(11);
    B->next->next=create(15);

    if(A->val>B->val)
    {
        temp1=A->next;
        temp2=B->next;
        head=B;
    }
    else
    {
        temp1=B->next;
        temp2=A->next;
        head=A;
    }

    while(A!=NULL)
    {
        if(A->val<temp2->val)
        {
            B->next=A;
            A->next=temp2;
            B=A;
            A=temp1;
            temp1=temp1->next;
            printf("hi");
        }
        else
        {
            B=temp2;
            temp2=temp2->next;
        }
    }

    while(head!=NULL)
    {
        printf("%d",head->val);
        head=head->next;
    }
}
