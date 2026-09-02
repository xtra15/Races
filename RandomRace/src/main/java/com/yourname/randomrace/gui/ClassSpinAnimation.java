package com.yourname.randomrace.gui;

import com.yourname.randomrace.RandomRacePlugin;
import com.yourname.randomrace.managers.ClassAssignmentManager;
import com.yourname.randomrace.managers.ClassPoolManager;
import com.yourname.randomrace.utils.MessageUtil;
import com.yourname.randomrace.utils.SoundUtil;
import me.athlaeos.valhallaraces.Class;
import me.athlaeos.valhallaraces.Race;
import me.athlaeos.valhallaraces.RaceManager;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.Sound;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.HandlerList;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.scheduler.BukkitTask;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class ClassSpinAnimation implements Listener {
    private static final int SLOTS = 3;
    private static final int CENTER = 1;
    private static final int[][] PHASES = {{2, 5}, {4, 3}, {8, 2}};
    private static final int TOTAL_TICKS;
    static {
        int t = 0;
        for (int[] p : PHASES) t += p[1];
        TOTAL_TICKS = t;
    }

    private final RandomRacePlugin plugin;
    private final Player player;
    private final Map<Integer, Class> winners;
    private final ClassPoolManager poolManager;
    private final ClassAssignmentManager assignmentManager = new ClassAssignmentManager();
    private final Map<Integer, String> groupNames = new LinkedHashMap<>();
    private Inventory inventory;
    private BukkitTask task;
    private boolean completed = false;

    public ClassSpinAnimation(RandomRacePlugin plugin, Player player, Map<Integer, Class> winners) {
        this.plugin = plugin;
        this.player = player;
        this.winners = winners;
        this.poolManager = plugin.getClassPoolManager();
        loadGroupNames();
    }

    private void loadGroupNames() {
        for (int g = 1; g <= 10; g++) {
            groupNames.put(g, plugin.getConfig().getString("groups." + g, "Group " + g));
        }
    }

    public void start() {
        inventory = plugin.getServer().createInventory(null, SLOTS, MessageUtil.color("&8Random Classes"));
        Bukkit.getPluginManager().registerEvents(this, plugin);
        player.openInventory(inventory);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        rollNext(winners.keySet().iterator());
    }

    private void rollNext(final java.util.Iterator<Integer> groups) {
        if (!groups.hasNext()) {
            finish();
            return;
        }
        final int group = groups.next();
        final Class winner = winners.get(group);
        SoundUtil.play(player, Sound.BLOCK_CHEST_OPEN);
        final int[] tick = {0};
        task = plugin.getServer().getScheduler().runTaskTimer(plugin, () -> {
            for (int slot = 0; slot < SLOTS; slot++) {
                int idx = tick[0] + slot;
                inventory.setItem(slot, iconFor(winner, group, idx));
            }
            SoundUtil.play(player, Sound.UI_BUTTON_CLICK);
            tick[0]++;
            if (tick[0] >= TOTAL_TICKS) {
                task.cancel();
                inventory.setItem(CENTER, iconFor(winner, group, TOTAL_TICKS));
                SoundUtil.play(player, Sound.BLOCK_NOTE_BLOCK_PLING);
                sendGroupMessage(group, winner);
                plugin.getServer().getScheduler().runTaskLater(plugin, () -> rollNext(groups), 12L);
            }
        }, 10L, 2L);
    }

    private ItemStack iconFor(Class winner, int group, int lane) {
        List<Class> cands = poolManager.candidatesFor(group, player, playerRace());
        if (!cands.isEmpty()) {
            Class shown = cands.get(lane % cands.size());
            return new ItemStack(configuredMaterial(shown), 1);
        }
        return new ItemStack(configuredMaterial(winner), 1);
    }

    private String playerRace() {
        Race r = RaceManager.getRace(player);
        return r == null ? null : r.getName();
    }

    private Material configuredMaterial(Class c) {
        String name = c != null ? plugin.getConfig().getString("class-materials." + c.getName()) : null;
        if (name != null) {
            Material m = Material.matchMaterial(name);
            if (m != null) return m;
        }
        if (c != null && c.getIcon() != null && c.getIcon().getType() != Material.AIR) return c.getIcon().getType();
        return Material.PAPER;
    }

    private void sendGroupMessage(int group, Class winner) {
        String gn = groupNames.getOrDefault(group, "Group " + group);
        String msg = MessageUtil.replace("{class}", stripColor(winner.getDisplayName()),
                MessageUtil.replace("{group}", gn,
                        plugin.getConfig().getString("messages.class-assigned", "&eYou are now a &b{group} {class}&e!")));
        player.sendMessage(MessageUtil.color(msg));
    }

    private void finish() {
        completed = true;
        HandlerList.unregisterAll(this);
        assignmentManager.assign(player, new ArrayList<>(winners.values()));
        List<String> parts = new ArrayList<>();
        for (Map.Entry<Integer, Class> e : winners.entrySet()) {
            parts.add(groupNames.getOrDefault(e.getKey(), "Group " + e.getKey()) + " " + stripColor(e.getValue().getDisplayName()));
        }
        String summary = MessageUtil.replace("{classes}", String.join(", ", parts),
                plugin.getConfig().getString("messages.class-summary", "&aYour classes are now: &e{classes}&a!"));
        player.sendMessage(MessageUtil.color(summary));
        SoundUtil.play(player, Sound.ENTITY_FIREWORK_ROCKET_BLAST);
        if (plugin.getConfig().getBoolean("broadcast-class", true)) {
            String bc = MessageUtil.replace("{player}", player.getName(),
                    plugin.getConfig().getString("messages.class-broadcast", "&e{player} &ahas been destined with their classes!"));
            Bukkit.broadcastMessage(MessageUtil.color(bc));
        }
    }

    private String stripColor(String s) {
        if (s == null) return "";
        return s.replaceAll("(?i)\\u00A7[0-9a-fk-or]", "");
    }

    @EventHandler
    public void onClose(InventoryCloseEvent e) {
        if (e.getPlayer().getUniqueId().equals(player.getUniqueId()) && !completed) {
            if (task != null) task.cancel();
            HandlerList.unregisterAll(this);
        }
    }

    @EventHandler
    public void onClick(InventoryClickEvent e) {
        if (e.getWhoClicked().getUniqueId().equals(player.getUniqueId())) {
            e.setCancelled(true);
        }
    }
}
