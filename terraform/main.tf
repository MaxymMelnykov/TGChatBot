provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "tg_bot_server" {
  ami           = "ami-0abcdef1234567890" # Підібрати під свій регіон
  instance_type = "t2.micro"
  key_name      = "your-ssh-key"

  tags = {
    Name = "TelegramBotServer"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt update",
      "sudo apt install -y docker.io",
      "git clone https://github.com/yourrepo/tg-bot.git",
      "cd tg-bot",
      "docker-compose up -d"
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
