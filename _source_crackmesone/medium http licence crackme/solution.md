# medium http licence crackme Writeup

Challenge_URL: https://crackmes.one/crackme/69917e2d853c2615340abd81

using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

class Program
{
    static void Main()
    {
        string ivBase64 = "Dx0NVfqhxJuQX+6unOnalA==";
        string dataBase64 = "YEHpXIjXhni1s0w/KPQi4a5BqUs/MWB/oWGgbjRiLqKT9jYUZ4oliUohKhktKnoBMSZTVbVt7f83hDxjeVkhivryPEqMgQ6BYxbGwaz+l/1wPfQpu6yRTG9CJRmoy8KzDVJVGXGBAMofp5yxnCc41w==";

        byte[] key;
        using (SHA256 sha = SHA256.Create())
        {
            key = sha.ComputeHash(Encoding.UTF8.GetBytes("t.me/junk_code"));
        }

        byte[] iv = Convert.FromBase64String(ivBase64);
        byte[] cipherText = Convert.FromBase64String(dataBase64);

        using (Aes aes = Aes.Create())
        {
            aes.Key = key;
            aes.IV = iv;
            aes.Mode = CipherMode.CBC;
            aes.Padding = PaddingMode.PKCS7;

            using (var decryptor = aes.CreateDecryptor())
            using (var ms = new MemoryStream(cipherText))
            using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
            using (var sr = new StreamReader(cs))
            {
                string result = sr.ReadToEnd();
                Console.WriteLine(result);
            }
        }
    }
}
