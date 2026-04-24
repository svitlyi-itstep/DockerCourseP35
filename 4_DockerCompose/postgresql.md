## Рекомендації щодо роботи з PostgreSQL

Приклад моделі **User**:

```C#
using System.ComponentModel.DataAnnotations;

public enum UserRole
{
    User,
    Moderator,
    Admin
}

public class User
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(100)]
    public string Username { get; set; } = null!;

    [Required]
    [MaxLength(255)]
    public string PasswordHash { get; set; } = null!;

    [Required]
    public UserRole Role { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    // Зв'язок з RefreshToken
    public List<RefreshToken> RefreshTokens { get; set; } = new();
}
```

Приклад моделі **RefreshToken**:

```C#
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

public class RefreshToken
{
    [Key]
    public int Id { get; set; }

    [Required]
    [MaxLength(500)]
    public string Token { get; set; } = null!;

    [Required]
    public DateTime ExpiresAt { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? RevokedAt { get; set; }

    // Зв`язок з User
    public int UserId { get; set; }
    public User User { get; set; } = null!;
}
```

Налаштування у DbContext для цих моделей:
```C#
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public DbSet<User> Users { get; set; }
    public DbSet<RefreshToken> RefreshTokens { get; set; }

    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    // Метод для налаштування роботи БД
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // User
        modelBuilder.Entity<User>(entity =>
        {
            entity.ToTable("users");

            entity.HasIndex(u => u.Username)
                .IsUnique();

            entity.Property(u => u.Role)
                .HasConversion<string>(); // enum → string

            entity.Property(u => u.CreatedAt)
                .HasColumnType("timestamp with time zone");
        });

        // RefreshToken
        modelBuilder.Entity<RefreshToken>(entity =>
        {
            entity.ToTable("refresh_tokens");

            entity.HasIndex(rt => rt.Token)
                .IsUnique();

            entity.HasOne(rt => rt.User)
                .WithMany(u => u.RefreshTokens)
                .HasForeignKey(rt => rt.UserId)
                .OnDelete(DeleteBehavior.Cascade);

            entity.Property(rt => rt.ExpiresAt)
                .HasColumnType("timestamp with time zone");

            entity.Property(rt => rt.CreatedAt)
                .HasColumnType("timestamp with time zone");
        });
    }
}
```