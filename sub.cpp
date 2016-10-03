#include<bits/stdc++.h>
using namespace std;

int b[1000001];

int main()
{
    //freopen("input10.txt", "r", stdin);
    //freopen("output10.txt", "w", stdout);
    long long a, n, k, r;
    scanf("%lld %lld %lld", &a, &n, &k);

    for(int i = 1; i <= min(n, k); i++)
        b[(a * i) % k] += ((n - i) / k) + 1;

    r = 1LL * b[0] * (b[0] - 1);
    for(int i = 1; i < k; i++)
        if(k - i != i)
            r += (1LL * b[k - i] * b[i]);
        else
            r += (1LL * b[i] * (b[i] - 1));
    r >>= 1LL;

    printf("%lld\n", r);
    return 0;
}
